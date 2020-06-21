#include "CommunicationManager.h"
namespace VMTDriver {
	//送受信スレッド
	std::mutex CommunicationWorkerMutex;
	std::deque<string> CommunicationWorkerReadQue;
	std::deque<string> CommunicationWorkerWriteQue;
	bool CommunicationWorkerExit = false;
	std::thread *CommunicationWorkerThread;
	void CommunicationWorker()
	{
		while (!CommunicationWorkerExit)
		{
			//クリティカルセクション
			{
				std::lock_guard<std::mutex> lock(CommunicationWorkerMutex); 

				//受信データがあったらひたすら読み込む
				string r = CommunicationManager::GetInstance()->GetSM()->readM2D();
				//受信データが有る場合(かつリミッター以下の場合)
				if (r != "" && CommunicationWorkerReadQue.size() < 1024) {
					CommunicationWorkerReadQue.push_back(r);
					//空になるまで待ち時間最短で読み込む
					continue;
				}
				//送信データがあったらひたすら書き込む
				if (!CommunicationWorkerWriteQue.empty())
				{
					if (CommunicationManager::GetInstance()->GetSM()->writeD2M(CommunicationWorkerWriteQue.front()) == true)
					{
						//成功したら引き抜いて続ける
						CommunicationWorkerWriteQue.pop_front();
						continue;
					}
					//書き込み失敗時は次の周期まで待つ(相手が起動していないか、相手がいっぱいいっぱい)
				}
			}
			//ノンクリティカルセクション
			Sleep(4); //240fps
		}
	}

	string CommunicationRead() {
		string r = "";
		//クリティカルセクション
		{
			std::lock_guard<std::mutex> lock(CommunicationWorkerMutex);
			if (!CommunicationWorkerReadQue.empty())
			{
				//受信キューから取り出し
				r = CommunicationWorkerReadQue.front();
				CommunicationWorkerReadQue.pop_front();
			}
		}
		return r;
	}
	void CommunicationWrite(string s) {
		std::lock_guard<std::mutex> lock(CommunicationWorkerMutex);
		if (CommunicationWorkerWriteQue.size() < 1024) { //1024件以上は捨てる(異常時、通信不良時)
			CommunicationWorkerWriteQue.push_back(s);
		}
	}

	CommunicationManager* CommunicationManager::GetInstance()
	{
		static CommunicationManager cm;
		return &cm;
	}
	SharedMemory::SharedMemory* CommunicationManager::GetSM()
	{
		return m_sm;
	}
	void CommunicationManager::Open()
	{
		if (m_opened) {
			return;
		}
		m_sm = new SharedMemory::SharedMemory();
		if (!m_sm->open()) {
			//オープンに失敗
			delete m_sm;
			m_sm = nullptr;
			return;
		}
		
		CommunicationWorkerThread = new std::thread(CommunicationWorker);
		m_opened = true;
	}
	void CommunicationManager::Close()
	{
		CommunicationWorkerExit = true;
		CommunicationWorkerThread->join();
		m_sm->close();
		delete m_sm;
		m_sm = nullptr;
		m_opened = false;
	}
	void CommunicationManager::Process(ServerTrackedDeviceProvider* server)
	{
		//通信の準備ができていない
		if (m_sm == nullptr) {
			return;
		}
		try {
			//受信(バッファが溜まっている場合高速に処理する)
			do {
				string r = CommunicationRead();
				if (r.empty()) {
					break;
				}
				//Log::printf("CommunicationWorkerReadQue:%d", CommunicationWorkerReadQue.size());

				json j = json::parse(r);
				string type = j["type"];
				if (type == "Pos") {
					string j2s = j["json"];
					json j2 = json::parse(j2s);


					DriverPose_t pose{ 0 };
					pose.deviceIsConnected = true;
					pose.poseIsValid = true;
					pose.result = TrackingResult_Running_OK;

					pose.qRotation = VMTDriver::HmdQuaternion_Identity;
					pose.qWorldFromDriverRotation = VMTDriver::HmdQuaternion_Identity;
					pose.qDriverFromHeadRotation = VMTDriver::HmdQuaternion_Identity;

					pose.vecPosition[0] = j2["x"];
					pose.vecPosition[1] = j2["y"];
					pose.vecPosition[2] = j2["z"];
					pose.qRotation.x = j2["qx"];
					pose.qRotation.y = j2["qy"];
					pose.qRotation.z = j2["qz"];
					pose.qRotation.w = j2["qw"];
					server->GetDevices()[0].SetPose(pose);
				}
				printf("%s\n", type.c_str());
			} while (true);

			//送信
			/*
			json jw;
			jw["type"] = "Hello";
			jw["json"] = json{ {"msg","Hello from cpp"} }.dump();
			CommunicationWrite(jw.dump());
			*/
		}
		catch (...) {
			m_sm->logError("Exception in CommunicationManager::Process");
		}
	}
}